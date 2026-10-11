from account_system import AccountSystem
from payment import Payment
from shopping_cart import ShoppingCart

def main():
    print("Welcome to the system!")

    system = AccountSystem()

    testProductIDArray = [1, 14, 8, 7]
    testQuantityArray = [1, 3, 2, 10]

    current_user = None

    while True:
        choice = input("\nEnter 'account' for account system, 'payment' to pay, or 'q' to quit:\n")

        if choice.lower() == "account":
            user = system.accountPage()
            if user:
                current_user = user
                print(f"Stored logged-in user in main: {current_user}")
        
        elif choice.lower() == "payment":
            if (current_user != None):
                pay = Payment()
                pay.payment(current_user)
            else:
                print("\nYou must be logged in to access the payment gateway!\n")
        
        elif choice.lower() == "shopping cart":
            if (current_user != None):
                shoppingCart = ShoppingCart()
                shoppingCart.addToCart(1, 1)
                shoppingCart.addToCart(14, 3)
                shoppingCart.addToCart(8, 2)
                shoppingCart.addToCart(7, 9)
                shoppingCart.checkout(current_user)
            else:
                print("\nYou must be logged in to access the payment gateway!\n")
        
        elif choice.lower() == "q":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()