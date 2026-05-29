## Requirements
1. The parking lot should have multiple levels, each level with a certain number of parking spots.
2. The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
3. Each parking spot should be able to accommodate a specific type of vehicle.
4. The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
5. The system should track the availability of parking spots and provide real-time information to customers.



## Classes and Methods

### Parking lot
- handle where to put vehicles
- handle payment

### Payment strategy
- flat fee ($x per hour)
- varied on vehicle 

### Parking strategy
- nearest first
- furthest first
- best fit

### Parking ticket
- floor
- spot
- vehicle type
- entry time
- exit time

### Parking floor
- keeps track of 2d grid of parking spots
- gives next avaiable spot

### Parking spot
- keeps track of size
- keeps track of empty/not empty

### Vehicle
- car, motorcycle, truck
