Feature: Testing Item


Scenario: #1 User can find the item on item listing page
Given the specific product which want to check
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

When we access the item listing page
Then we will find "Giorgio Armani Women Idole Perfume"


Scenario: #2 User can find the item on item detail page
Given the specific product which want to check
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

When we access the item detail page of "99999"
Then we will find "Giorgio Armani Women Idole Perfume"

