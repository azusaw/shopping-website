Feature: User


Scenario: #1 Guest user can access the item listing page
Given I am not authenticated
When I access the item listing page
Then Status code is 200


Scenario: #2 Customer user can access the item listing page
Given I am a customer user
When I access the item listing page
Then Status code is 200


Scenario: #3 Staff user can access the item listing page
Given I am a staff user
When I access the item listing page
Then Status code is 200


Scenario: #4 Guest user can access the basket page
Given I am not authenticated
When I access the basket page
Then Status code is 200


Scenario: #6 Customer user can access the basket page
Given I am a customer user
When I access the basket page
Then Status code is 200


Scenario: #7 Staff user can not access the basket page
Given I am a staff user
When I access the basket page
Then Status code is 302


Scenario: #8 Guest user can not access the purchase page
Given I am not authenticated
When I access the purchase page
Then Status code is 302


Scenario: #9 Customer user can access the purchase page
Given I am a customer user
When I access the purchase page
Then Status code is 200


Scenario: #10 Staff user can not access the purchase page
Given I am a staff user
When I access the purchase page
Then Status code is 302


Scenario: #11 Guest user can not access the dashboard page
Given I am not authenticated
When I access the dashboard page
Then Status code is 302


Scenario: #12 Customer user can not access the dashboard page
Given I am a customer user
When I access the dashboard page
Then Status code is 302


Scenario: #13 Staff user can access the dashboard page
Given I am a staff user
When I access the dashboard page
Then Status code is 200


Scenario: #14 Guest user can not access the profile page
Given I am not authenticated
When I access the profile page
Then Status code is 302


Scenario: #15 Customer user can access the profile page
Given I am a customer user
When I access the profile page
Then Status code is 200


Scenario: #16 Staff user can not access the profile page
Given I am a staff user
When I access the profile page
Then Status code is 302


Scenario: #17 Guest user can not access the order listing page
Given I am not authenticated
When I access the order listing page
Then Status code is 302


Scenario: #18 Customer user can access the order listing page
Given I am a customer user
When I access the order listing page
Then Status code is 200


Scenario: #19 Staff user can access the order listing page
Given I am a staff user
When I access the order listing page
Then Status code is 200