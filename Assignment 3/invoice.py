class Invoice:


    def createInvoice(self, paymentDetails, itemArray, quantityArray, priceArray):
        total = 0
        print("\n===== INVOICE =====\n")
        print("{:<25} {:>10} {:>10} {:>12}".format("Product", "Quantity", "     Price", "Subtotal"))
        print("-" * 60)
        
        for i in range(len(itemArray)):
            subtotal = quantityArray[i] * priceArray[i]
            total += subtotal
            print("{:<25} {:>10} {:>10.2f} {:>12.2f}".format(
                itemArray[i], quantityArray[i], priceArray[i], subtotal
            ))

        print("-" * 60)
        print("{:<25} {:>32.2f}".format("TOTAL", total))
        print("\nPayment Details:")
        for key, value in paymentDetails.items():
            print(f"{key}: {value}")
        print("\n===== END OF INVOICE =====\n")
        return