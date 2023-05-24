from django.contrib.auth.models import User
from pkgutil import get_data
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.views import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import *
from rest_framework.parsers import *
from django.db.models import Q
from .gpt import find
import json
import stripe
from django.http import HttpResponseRedirect

# ? this is the premium api link: price_1N9UJTIxwx5qMRmKjZwMsCM5
# ? premium plus api link: price_1N9UKQIxwx5qMRmK4MOJD67t

# & Here are the test keys
# Key: pk_test_51MuGyTIxwx5qMRmKVZUTpkjmN6a3S9V8uFqai4Pe1e3L8Vh5jLXTJUJQkR0G6fjT4Ei3GCSfOpKJjzah8SlukgQd00t7Xigbsb
# Secret key:
# sk_test_51MuGyTIxwx5qMRmKY7YJDm0Ho3DXP0gVYSQ6cnGGyuf8ZQ5P3jyMUc3T80UmnExJVQuNjJ3uEMPT05kROuIh9M9800W9of6tjw

stripe.api_key = 'sk_test_51MuGyTIxwx5qMRmKY7YJDm0Ho3DXP0gVYSQ6cnGGyuf8ZQ5P3jyMUc3T80UmnExJVQuNjJ3uEMPT05kROuIh9M9800W9of6tjw'
YOUR_DOMAIN = 'localhost:8000'
# Create your views here.
# Generate Token Manually


class Payment(APIView):
    def post(self, request):
        email = request.data['email']
        print(email)
        DOMAIN = "http://localhost:8000/api/create-portal-session"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': request.data['lookup_key'],
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=f'{DOMAIN}?success=true&email={email}&session_id=' +
            "{CHECKOUT_SESSION_ID}",
            cancel_url=f"{DOMAIN}?canceled=true",
        )
        return redirect(checkout_session.url)


class customer_portal(APIView):
    def get(self, request):
        # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
        # Typically this is stored alongside the authenticated user in your database.
        success = request.GET.get('success')
        checkout_session_id = request.GET.get('session_id')
        email = request.GET.get('email')
        checkout_session = stripe.checkout.Session.retrieve(
            checkout_session_id)
        return_url = ""

        print(email)
        if success is not None:
            print("Payment successful!")
            profile = ProfileData.objects.filter(email=email).last()
            price = int(checkout_session.amount_total)
            profile.account = "Starter" if price == 1995 else "Premium"
            profile.save()

            # ? saving credits per plan
            creds = 20000 if price == 1995 else 200000
            profile.save()
            credits(available=creds, user=email).save()

            return_url = f"http://localhost:3000/Payment?success=true&session_id={checkout_session_id}"
        else:
            print("Payment not successful!")
            return_url = f"http://localhost:3000/Payment?canceled=true"

        return redirect(return_url)


class webhook_received(APIView):
    def post(self, request):
        # Replace this endpoint secret with your endpoint's unique secret
        # If you are testing with the CLI, find the secret by running 'stripe listen'
        # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
        # at https://dashboard.stripe.com/webhooks
        webhook_secret = 'whsec_12345'
        request_data = json.loads(request.data)

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']
        data_object = data['object']

        print('event ' + event_type)

        if event_type == 'checkout.session.completed':
            print('🔔 Payment succeeded!')
        elif event_type == 'customer.subscription.trial_will_end':
            print('Subscription trial will end')
        elif event_type == 'customer.subscription.created':
            print('Subscription created %s', event.id)
        elif event_type == 'customer.subscription.updated':
            print('Subscription created %s', event.id)
        elif event_type == 'customer.subscription.deleted':
            # handle subscription canceled automatically based
            # upon your subscription settings. Or if the user cancels it.
            print('Subscription canceled: %s', event.id)

        return JsonResponse({'status': 'success'})


class getChatHistory(APIView):
    def get(self, request):
        user = request.GET.get('user')
        data = Chat.objects.filter(user=user).values()
        return Response({'data': data}, status=status.HTTP_200_OK)


class profileData(APIView):
    def get(self, request):
        email = request.GET.get('email')
        data = ProfileData.objects.filter(email=email).values().last()
        if data is None:
            data = ProfileData.objects.filter(pk=19).values().last()
        return Response({'data': data}, status=status.HTTP_200_OK)


class savePrompt(APIView):
    def get(self, request):
        user = request.GET.get('user')
        prompt_id = request.GET.get('id')
        cat = request.GET.get('category')
        # ? check if that category already exists otherwise create a  new one
        if (len(categories.objects.filter(name__icontains=cat)) == 0):
            categories(name=cat).save()
        # ? check if prompt is already saved
        try:
            savedPrompts.objects.get(
                pid=prompt_id, saved_by=user, category__icontains=cat)
            return Response({'msg': 'Prompt is already saved!'}, status=status.HTTP_201_CREATED)
        except:
            # get prompt first of same id
            prompt = Prompt.objects.get(id=prompt_id)
            savedPrompts(pid=prompt_id, Title=prompt.Title, Description=prompt.Description,
                         prompt_text=prompt.prompt_text, User=prompt.User, Views=prompt.Views, saved_by=user, img=prompt.img, category=cat).save()
            return Response({'msg': 'Your prompt has been saved!'}, status=status.HTTP_201_CREATED)


class getSavedPrompts(APIView):
    def get(self, request):
        user = request.GET.get('user')
        data = []

        categories_list = [
            category.name for category in categories.objects.all()]

        for cat in categories_list:
            prompts = savedPrompts.objects.filter(
                saved_by=user, category__icontains=cat).order_by('-Views').values()
            if len(prompts) > 0:
                data.append({
                    'name': cat,
                    'cat_prompts': prompts,
                })

        return Response({'prompts': data}, status=status.HTTP_200_OK)


class increaseView(APIView):
    def get(self, request):
        pk = request.GET.get('id')
        prompt = Prompt.objects.get(id=pk)
        prompt.Views = int(prompt.Views)+1
        prompt.save()

        # update saved prompts also
        prompts = savedPrompts.objects.filter(id=pk)
        for prompt in prompts:
            prompt.Views = int(prompt.Views)+1
            prompt.save()

        return Response(status=status.HTTP_200_OK)


class searchPrompt(APIView):
    def get(self, request):
        typ = request.GET.get('type')
        query = request.GET.get('query')
        user = request.GET.get('user')
        data = ''
        if typ == "community":
            data = Prompt.objects.filter(
                (Q(Title__icontains=query) | Q(Description__icontains=query))).order_by('-Views').values()
        elif typ == "user":
            data = Prompt.objects.filter(
                (Q(Title__icontains=query) | Q(Description__icontains=query)) & Q(User=user)).order_by('-Views').values()
        # saved prompts will be in else
        else:
            data = savedPrompts.objects.filter(
                (Q(Title__icontains=query) | Q(Description__icontains=query)) & Q(saved_by=user)).values()

        return Response({'prompts': data}, status=status.HTTP_200_OK)


class searchSavedPrompt(APIView):
    def get(self, request):
        query = request.GET.get('query')
        user = request.GET.get('user')
        data = []

        categories_list = [
            category.name for category in categories.objects.all()]

        for cat in categories_list:
            prompts = savedPrompts.objects.filter((Q(Title__icontains=query) | Q(
                Description__icontains=query)) & (Q(saved_by=user) & Q(category__icontains=cat))).order_by('-Views').values()
            print(len(prompts))
            if len(prompts) > 0:
                data.append({
                    'name': cat,
                    'cat_prompts': prompts,
                })

        return Response({'prompts': data}, status=status.HTTP_200_OK)


class Conversation(APIView):
    def get(self, request):
        query = request.GET.get('query')
        user = request.GET.get('user')
        prompt_id = request.GET.get('prompt_id')
        prompt_title = request.GET.get('prompt_title')
        checkChatExists = request.GET.get('exist')
        if (checkChatExists is not None):
            chat = Chat.objects.get(user=user, prompt_id=prompt_id)
            # just update query and response by appending at last of chat data set
            data = json.loads(chat.chat)
            return Response({'history': data}, status=status.HTTP_200_OK)

        response = find(query)
        # check if same chat already
        history = []
        try:
            chat = Chat.objects.get(user=user, prompt_id=prompt_id)
            # just update query and response by appending at last of chat data set
            data = json.loads(chat.chat)
            data.append({
                "query": query,
                "response": response,
            })
            chat.chat = json.dumps(data)
            chat.save()
            history = data

        except:
            Chat.objects.create(name=query, user=user, prompt_id=prompt_id,
                                prompt_title=prompt_title, chat=json.dumps(
                                    [{
                                        "query": query,
                                        "response": response,
                                    }]

                                ))

        words = str(response).split(' ')
        creds = credits.objects.filter().last()
        creds.available = creds.available-len(words)
        creds.save()

        # save query and response in CHAT model
        return Response({'input': query, 'output': response, 'history': history}, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class getUserPrompts(APIView):
    def get(self, request, email):
        data = Prompt.objects.filter(User=email).order_by('-Views').values()
        seria = PromptSerializer(data, many=True)
        return Response({'prompts': data}, status=status.HTTP_200_OK)


class getPrompt(APIView):
    def get(self, request, pk):
        data = Prompt.objects.get(id=pk)
        seria = PromptSerializer(data)
        return Response({'prompt': seria.data}, status=status.HTTP_200_OK)


class getPrompts(APIView):
    def get(self, request):
        data = Prompt.objects.all().order_by('-Views').values()
        return Response({'prompts': data}, status=status.HTTP_200_OK)


class createPrompt(APIView):
    def post(self, request):
        seria = PromptSerializer(data=request.data)
        if (seria.is_valid()):
            seria.save()
            return Response({'msg': 'Your prompt is now live!'}, status=status.HTTP_201_CREATED)


class uploadProfilePicture(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        # ?? getting account from profile DB
        account = ProfileData.objects.filter(
            email=request.data['email']).last().account
        request.data.update({'account': account})

        seria = profilePictureSerializer(data=request.data)
        image = ''
        if (seria.is_valid()):
            seria.save()
            image = image+str(ProfileData.objects.filter(
                email=request.data['email']).last().picture)
        return Response({'img': image}, status=status.HTTP_201_CREATED)


class UserRegistrationView(APIView):
    def post(self, request):
        seria = UserRegistrationSerializer(data=request.data)
        if (seria.is_valid()):
            ProfileData(email=request.data['email'], fname=request.data['name'].split(
                ' ')[0], lname=request.data['name'].split(' ')[1], account="Free").save()
            user = seria.save()
            token = get_tokens_for_user(user)

            # ? assigning the credits to user
            credits(available=1000, user=request.data["email"]).save()
            return Response({'token': token, 'msg': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Email already Exists.Try another Email!'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        seria = UserLoginSerializer(data=request.data)
        if (seria.is_valid()):
            email = seria.data.get('email')
            pas = seria.data.get('password')
            user = authenticate(email=email, password=pas)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Username or Password'}, status=status.HTTP_404_NOT_FOUND)

        return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seria = UserProfileSerializer(request.user)
        return Response(seria.data, status=status.HTTP_200_OK)
