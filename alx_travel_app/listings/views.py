from rest_framework import generics
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
import requests
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking, Payment


# Listing views
class ListingListCreate(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class ListingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'listng_id' # Note: your model uses 'listng_id'

# Booking views
class BookingListCreate(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'booking_id'

# Review views
class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'listing_id' # Adjust as needed
    


class InitiatePayment(APIView):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, booking_id=booking_id)
        CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')
        
        # Chapa API URL for initialization
        chapa_url = "https://api.chapa.co/v1/transaction/initialize"
        
        # Prepare the payment data
        data = {
            "amount": str(booking.listing_id.price),
            "currency": "ETB",  # Adjust currency as needed
            "email": "user@example.com", # Replace with actual user email
            "first_name": "First",
            "last_name": "Last",
            "tx_ref": f"booking-{booking.booking_id}-{os.urandom(4).hex()}", # Unique transaction reference
            "callback_url": f"http://127.0.0.1:8000/api/payments/verify/{booking.booking_id}/"
        }
        
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(chapa_url, json=data, headers=headers)
            response.raise_for_status()
            chapa_response = response.json()
            
            if chapa_response['status'] == 'success':
                # Create a Payment object in your database
                payment = Payment.objects.create(
                    booking=booking,
                    amount=booking.listing_id.price,
                    transaction_id=chapa_response['data']['tx_ref'],
                    status='pending'
                )
                
                return Response({
                    "status": "success",
                    "message": "Payment initiated successfully",
                    "checkout_url": chapa_response['data']['checkout_url']
                })
            else:
                return Response({
                    "status": "error",
                    "message": "Failed to initiate payment",
                    "error_details": chapa_response.get('message')
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPayment(APIView):
    def get(self, request, booking_id):
        try:
            booking = get_object_or_404(Booking, booking_id=booking_id)
            payment = get_object_or_404(Payment, booking=booking)
            CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')

            # Chapa API URL for verification
            chapa_url = f"https://api.chapa.co/v1/transaction/verify/{payment.transaction_id}"
            
            headers = {
                "Authorization": f"Bearer {CHAPA_SECRET_KEY}"
            }
            
            response = requests.get(chapa_url, headers=headers)
            response.raise_for_status()
            chapa_response = response.json()
            
            if chapa_response['status'] == 'success' and chapa_response['data']['status'] == 'success':
                payment.status = 'completed'
                payment.save()
                
                # Here, you would implement sending a confirmation email using Celery
                # For example: send_booking_confirmation_email.delay(booking.id)
                
                return Response({
                    "status": "success",
                    "message": "Payment verified and completed successfully."
                })
            else:
                payment.status = 'failed'
                payment.save()
                return Response({
                    "status": "failed",
                    "message": "Payment verification failed."
                })

        except (Booking.DoesNotExist, Payment.DoesNotExist) as e:
            return Response({"error": "Booking or Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Error verifying payment: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)