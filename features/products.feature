#features/products.feature
$featureContent = @'
Feature: Product Management
  As a Store Manager
  I want to manage products
  So that I can keep track of my inventory

  Background:
    Given the following products
      | name          | description        | price | category    | available |
      | Laptop        | High-end laptop   | 999.99| Electronics | true      |
      | Mouse         | Wireless mouse    | 29.99 | Electronics | true      |
      | T-Shirt       | Cotton t-shirt    | 19.99 | Clothing    | true      |
      | Python Book   | Programming book  | 49.99 | Books       | false     |

  Scenario: Create a product
    When I create a new product with name "Headphones", description "Noise cancelling", price "199.99", category "Electronics", available "true"
    Then I should see the product "Headphones" in the results

  Scenario: Read a product
    When I request product with id "1"
    Then I should get product "Laptop"

  Scenario: Update a product
    When I update product "1" with name "Gaming Laptop", description "High performance"
    Then I should see product "1" with name "Gaming Laptop"

  Scenario: Delete a product
    When I delete product "2"
    Then I should not see product "Mouse" in the results

  Scenario: List all products
    When I list all products
    Then I should see 4 products

  Scenario: List products by category
    When I search for products in category "Electronics"
    Then I should see 2 products
    And I should see "Laptop" in the results
    And I should see "Mouse" in the results

  Scenario: List products by availability
    When I search for available products
    Then I should see 3 products
    And I should not see "Python Book" in the results

  Scenario: List products by name
    When I search for products named "Laptop"
    Then I should see 1 product
    And I should see "Laptop" in the results
'@

$featureContent | Out-File -FilePath features/products.feature -Encoding utf8 -NoNewline