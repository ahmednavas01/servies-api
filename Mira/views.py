from django.shortcuts import render,redirect
import smtplib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pyotp
from .models import UserLogin
import requests
from bs4 import BeautifulSoup




# Generate a new OTP secret
totp = pyotp.TOTP(pyotp.random_base32())
secret = totp.secret
# print(f"Your OTP secret is: {secret}")

# Generate OTP code
otp_code = totp.now()
# print(f"Your OTP code is: {otp_code}")

# Verify OTP code
def verify_otp(otp_code, secret):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp_code)


def email_sent(otp,email):
    mail = smtplib.SMTP('smtp.gmail.com', 587)  # host and port area
    mail.ehlo()  # Hostname to send for this command defaults to the FQDN of the local host.
    mail.starttls()  # security connection
    mail.login('ahamednawas05@gmail.com', 'aaxa vsmv tlku kegc')  # login part
    mail.sendmail('ahamednawas05@gmail.com', email, f"Navas Gpt one time otp {otp}")  # send part
    # print("Congrates! Your mail has send. ")


def index(request):

    email = request.session.get('email', False)


    if 'gpt' in request.POST:

        user_email = request.POST['email']
        filter = UserLogin.objects.filter(user_email=user_email,user_status=False).exists()
        user_data = UserLogin.objects.filter(user_email=user_email).values()
        if filter:
            print("access")
            request.session['user_email'] = user_email
            UserLogin.objects.filter(user_email=user_email).update(
                user_status=True)


            # list(user_data)[0]['user_request']



            return redirect('gpt')

    elif request.method=='POST':
        print("kk")

        return render(request, "mira/index.html", context={"email": "hello"})
    return render(request,"mira/index.html",context={"email": email})


def logout(request):
    email = request.session.get('user_email', False)
    request.session['email'] = False
    if email:
        request.session['user_email'] = False
        UserLogin.objects.filter(user_email=email).update(
            user_status=False)
        return redirect('login')
def signup(request):
    if  'verify' in request.POST:
        email=request.POST["email"]
        request.session['user_email']=email
        email_sent(secret,email)

        return render(request, "mira/signup.html", context={"code": "hello",'email_verify':email})

    elif 'create' in request.POST:

        otp=request.POST["otp"]

        if otp==secret:
            request.session['email'] = 'hello'
            email = request.session.get('user_email')

            filter=UserLogin.objects.filter(user_email=email).exists()

            if not (filter):

                UserLogins=UserLogin()
                UserLogins.user_email=email
                UserLogins.user_request=0
                UserLogins.save()

                return redirect('login')

            return redirect('signup')
        else:
            return redirect('signup')

    return render(request,'mira/signup.html',)


def GPT(request):
    email = request.session.get('user_email', False)
    filter = UserLogin.objects.filter(user_email=email, user_status=False).exists()
    print(email,filter,"//")
    if filter or email:
        return render(request,'mira/gpt.html')

    else:
        return redirect('login')


def genarative_text(text):

    text_list=[]


    from groq import Groq

    client = Groq(
        api_key="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",
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        # print(chunk.choices[0].delta.content or "",end='')
        text_list.append(chunk.choices[0].delta.content or "")

    complete_message = ' '.join(text_list)

    return complete_message















@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Example logic for bot response (replace with your logic)
        text=genarative_text(user_message)


        response_data = {
            'user_message': user_message,
            'bot_response': text
        }
        # print(text in "<html><head>" , "ll")
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})




def beautiful_soup():
    from bs4 import BeautifulSoup

    # Example HTML content
    html_content = """
    <html>
        <head><title>Sample Page</title></head>
        <body>
            <h1>Hello, World!</h1>
            <p>This is a sample page.</p>
            <a href="http://example.com">Example</a>
        </body>
    </html>
    """

    # Parse the HTML content
    response = requests.get('https://www.google.com/maps/place/Chennai')

    soup = BeautifulSoup( response.content, 'html.parser')
    script_tag = soup.find('script', )

    # Print the parsed HTML
    print(script_tag.string)

# beautiful_soup()

