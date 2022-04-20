from config.models import InsuranceApiUrlConfig


# Third Party URL's
def ThirdPartyQoute():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='ThirdPartyQoute')
    print(data.api_url)
    return data.api_url


def ThirdPartyPayment():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='ThirdPartyPayment')
    return data.api_url


def ThirdPartyPolicy():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='ThirdPartyPolicy')
    return data.api_url


# Licensing API URL's
def ZinaraQuote():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='ZinaraQuote')
    return data.api_url


def RadioQuote():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='RadioQuote')
    return data.api_url


def LicensingPayment():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='LicensingPayment')
    return data.api_url


def LicensingPolicy():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='LicensingPolicy')
    return data.api_url


# Combo API URL's
def ThirdPartyZinaraQoute():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='ThirdPartyZinaraQoute')
    return data.api_url


def ThirdPartyZinaraPayment():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='ThirdPartyZinaraPayment')
    return data.api_url


def ThirdPartyZinaraPolicy():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='ThirdPartyZinaraPolicy')
    return data.api_url


# Check if Vehicle is registered
def CheckVehicle():
    data = InsuranceApiUrlConfig.objects.get(key_identifier='CheckVehicle')
    return data.api_url
