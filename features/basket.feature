Feature: Testing Item


Scenario: #1 User can add the item into basket in item detail page
Given the specific product which want to add into basket
     | key             | value |
     | item_id         | 99999 |
     | gender          | Women |
     | master_category | Personal Care |
     | sub_category    | Fragrance |
     | article_type    | Perfume and Body Mist |
     | base_colour     | Gold |
     | hex_code        | #ffd700 |
     | year            | 2017 |
     | season          | Spring |
     | usage           | Casual |
     | display_name    | Giorgio Armani Women Idole Perfume |
     | price           | 50.00 |
     | link            | http://assets.myntassets.com/v1/images/style/properties/b0d3dcd6aaa7274486236fa267ef8cb5_images.jpg |

When we add the item with id "99999" into basket
Then we will be redirected to the basket page

Scenario: #1 User can add the item into basket in item detail page
Given the specific product which want to add into basket
     | key             | value |
     | item_id         | 99999 |
     | gender          | Women |
     | master_category | Personal Care |
     | sub_category    | Fragrance |
     | article_type    | Perfume and Body Mist |
     | base_colour     | Gold |
     | hex_code        | #ffd700 |
     | year            | 2017 |
     | season          | Spring |
     | usage           | Casual |
     | display_name    | Giorgio Armani Women Idole Perfume |
     | price           | 50.00 |
     | link            | http://assets.myntassets.com/v1/images/style/properties/b0d3dcd6aaa7274486236fa267ef8cb5_images.jpg |

When we add the item with id "99999" into basket
When we update the item quantity to "20"
Then item quantity will be updated to "20"


Scenario: #3 User can process a purchase after adding item
Given the specific product which want to add into basket
     | key             | value |
     | item_id         | 99999 |
     | gender          | Women |
     | master_category | Personal Care |
     | sub_category    | Fragrance |
     | article_type    | Perfume and Body Mist |
     | base_colour     | Gold |
     | hex_code        | #ffd700 |
     | year            | 2017 |
     | season          | Spring |
     | usage           | Casual |
     | display_name    | Giorgio Armani Women Idole Perfume |
     | price           | 50.00 |
     | link            | http://assets.myntassets.com/v1/images/style/properties/b0d3dcd6aaa7274486236fa267ef8cb5_images.jpg |

When we add the item with id "99999" into basket
When we process a purchase
Then we will be redirected to login page

