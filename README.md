## nork town challenge

### **Technologies/Frameworks/Libs used:**

- Flask[async]
- pydantic - data validation
- loguru - logs
- python-decouple - files .env
- pytest-asyncio, pytest-cov, unittest and mutatest - for unit tests
- sqlite3 - database
- sqlalchemy - ORM map

### Step one
#### create a virtual environment
Create and start a virtual env for the project. 

- To create the virtual environment, run:
```bash
python3 -m venv env
```
- To activate the virtual environment run:

    Linux:
    ```bash
    source env/bin/activate
    ```
    Windows:
    ```shell
    env\Scripts\activate.bat
    ```

### Step two
#### Installation of dependencies
1. __Install the packages in the virtual environment from the following command:__
    
    ```bash
    pip install -r requirements.txt
    ```  
    __or if you are going to run the tests:__
    ```bash
    pip install -r requirements-dev.txt
    ```
   ```bash
    run bash mutation_test.sh
    ``` 

### Step three
#### Create environment variables

1. Create a `.env` file in the project root, following this template:

~~~
HOST_URL=sqlite:///server.db
CAR_LIMIT=2
~~~

### Step four
#### Run project

1. To start the hypercorn server you need to be at the project root in the terminal and run the following command
 ~~~
    flask --app main.py run --host "0.0.0.0" -p 5000
    
    Or just run in terminal "python3 main.py"
 ~~~

2. You can change the HOST and PORT as you wish in command line, main.py or dockerfile.

## **Endpoints:**

### "/customers"

> _Endpoint to get all registered customers_

## Requisition

#### **request template on route HTTP:**
~~~
http:{host}/customers
~~~

## Response

#### **response template:**

```json
{
  "result": ["list of customers"],
  "success": "request success, True or False",
}
```

## Example

#### Response:

```json
{
  "success": true,
  "result": {
    "customers": [
      {
        "id": 1,
        "name": "Larissa Reis",
        "email": "vih-reis@hotmail.com",
        "sale_opportunity": false
      },
      {
        "id": 2,
        "name": "Vinicius Dos Reis Oliveira",
        "email": "vini@123.com",
        "sale_opportunity": true
      },
      {
        "id": 3,
        "name": "Otavio",
        "email": "teste@teste.com",
        "sale_opportunity": true
      },
      {
        "id": 4,
        "name": "fulano",
        "email": "fulano@teste.com",
        "sale_opportunity": true
      },
      {
        "id": 5,
        "name": "beltrano",
        "email": "beltrano@teste.com",
        "sale_opportunity": false
      }
    ]
  }
}
```

### "/cars"

> _Endpoint to get all registered cars_

## Requisition

#### **request template on route HTTP:**
~~~
http:{host}/cars
~~~

## Response

#### **response template:**

```json
{
  "result": ["list of cars"],
  "success": "request success, True or False",
}
```

## Example

#### Response:

```json
{
  "success": true,
  "result": {
    "cars": [
      {
        "id": 2,
        "color": "blue",
        "model": "hatch",
        "customer_id": 1
      },
      {
        "id": 3,
        "color": "yellow",
        "model": "convertible",
        "customer_id": 1
      },
      {
        "id": 4,
        "color": "blue",
        "model": "sedan",
        "customer_id": 1
      },
      {
        "id": 5,
        "color": "blue",
        "model": "sedan",
        "customer_id": 5
      },
      {
        "id": 6,
        "color": "blue",
        "model": "sedan",
        "customer_id": 5
      }
    ]
  }
}
```


### "/customer/register"

> _Endpoint to register a new customer_

## Requisition

#### **request template on route HTTP:**
~~~
http:{host}//customer/register
~~~
#### **body:**
```json
{
    "name": "beltrano",
    "email": "beltrano@teste.com"
    "sale_opportunity": "false"
}
```
~~~
the parameter sale_opportunity can be or not informed, by default is True
~~~

## Response

#### **response template:**

```json
{
  "message": "message to detail certain responses",
  "success": "request success, True or False",
}
```

## Example


#### Response:
```json
{
    "success": true,
    "message": "buyer_management registered successfully"
}
```

### "/linking-car/<customer_id>"

> _Endpoint linking a car to an owner_

## Requisition

#### **request template on route HTTP:**
~~~
http:{host}//linking-car/1
~~~
#### **body:**
```json
{
    "color": "blue",
    "model": "sedan"
}
```
~~~
you can only link a car to a customer_id that already exists
~~~

## Response

#### **response template:**

```json
{
  "message": "message to detail certain responses",
  "success": "request success, True or False",
}
```

## Example


#### Response:
```json
{
    "success": true,
    "message": "successfully registered car"
}
```
