class CheckoutInfoFactory:
    @staticmethod
    def get_valid_info():
        return {
            "first_name": "Morpheus",
            "last_name": "StillNoIdea",
            "postal_code": "1010"
        }


    @staticmethod
    def get_invalid_info():
        return {
            "first_name": "",
            "last_name": "",
            "postal_code": ""
        }