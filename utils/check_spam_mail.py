import joblib

# Load the pre-trained vectorizer and spam detection model
vectorizer = joblib.load("utils/vectorizer.joblib")
model = joblib.load("utils/spam_detection_model.joblib")

def check_spam_mail(mail):

    # Transform the input mail into features using the vectorizer
    mail_features = vectorizer.transform([str(mail)])

    # Make a prediction using the model
    prediction = model.predict(mail_features)

    # Check if the prediction indicates spam (0) and not spam (1)
    if prediction[0]==1:
        return False
    return True