from django import forms

class inputweb(forms.Form):
    num1=forms.IntegerField(min_value=2,max_value=100,label="Enter Number")
