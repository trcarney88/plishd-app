# Plishd
Source code for plishd.com

## Overview of Plishd
Plishd is a work accomplishment tracking app. It allows the user to track what they do at work to make writing a resume or aceing a performance evaluation easier by collecting what you do at work in a more presentable format. The ideal user will set up notifications based on their preferences, add accomplishments, and then use the pdf generator to create a report of their accomplishments to reach their career goals. Users can set the period between notifications, the time they will receive the notification, and the method in which they will receive the notification (currently only text message and email).

## Technical Information about Plishd
Plishd is built using Django 2.2.6. The database used for the site can be either sqlite or AWS RDS depending on if the RDS credential are filled out in the private config file. A template was used for the front end of the site. The template used was TheSaas from The Themeio, https://themeforest.net/item/thesaas-responsive-bootstrap-saas-software-webapp-template/19778599. It is a bootstrap based theme. Components and the basic page layout were taken from the theme but the linking of the front end to the back end and the creation of the actual pages were performed by me. Payments are processed using Stripe.

## Evaluating Plishd
If you would like to evaluate plishd.com and have no intention of using it full time, you can create a dummy account. There is no email verification at sign up, feel free to make an account with fake information
