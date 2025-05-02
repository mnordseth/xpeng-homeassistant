# Xpeng Home Assistant Integration
This component intergrates Xpeng cars into Home Assistant via the Enode service.

## Key Features

### Comprehensive Vehicle Monitoring
- **Battery Management**: Real-time battery level tracking with customizable alerts
- **Charging Intelligence**: Monitor charging status, power delivery, and set charging notifications
- **Location Awareness**: Keep track of your vehicle's location and create location-based automations
- **Vehicle Analytics**: Access detailed information including range, odometer, and charging efficiency

## Requirements
- XPENG Electric Vehicle (Compatible with all models)
- Enode API Access (Credentials required for setup)

## Setup Guide
1. Create an Enode developer account at https://www.enode.io/
2. Request production access from Enode for your developer account
3. Create a new application in your Enode developer dashboard
4. Get your Client ID and Client Secret from the Enode dashboard
5. Add this repository as a custom repository inside HACS settings. Make sure you select Integration as Category.
6. Add the Xpeng integration to Home Assistant and provide your Client ID and Client Secret