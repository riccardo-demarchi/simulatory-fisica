import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j0, j1, y0, y1

def create_data(N, w):
    """
    Creates a dataset with noise having a linear relationship with the target values.
    N: number of samples
    w: target values
    """
    # Feature matrix with random data
    X = np.random.rand(N, 1) * 10
    # target values with noise normally distributed
    y = w[0] * X + w[1] + np.random.randn(N, 1)
    return X, y
    # Visualize the data
    X, y = create_data(200, [2, 1])
    plt.figure(figsize=(10, 6))
    plt.title('Simulated Linear Data')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.scatter(X, y)
    plt.show()
    return X, y

def create_time_series(N, w):
    """
    Creates a time series data with a linear trend and a seasonal component.
    N: number of samples
    w: target values
    """
    # time values
    time = np.arange(0,N)
    # linear trend
    trend = time * w[0]
    # seasonal component
    seasonal = np.sin(time * w[1])
    # noise
    noise = np.random.randn(N)
    # target values
    y = trend + seasonal + noise
    return time, y

    # Visualize the data
    time, y = create_time_series(100, [0.25, 0.2])

    plt.figure(figsize=(10, 6))
    plt.title('Simulated Time Series Data')
    plt.xlabel('Time')
    plt.ylabel('y')

    plt.plot(time, y)
    plt.show()


def create_fake_data(N):
    """
    Creates a dataset with fake data.
    N: number of samples
    """
    fake = Faker()
    names = [fake.name() for _ in range(N)]
    addresses = [fake.address() for _ in range(N)]
    emails = [fake.email() for _ in range(N)]
    phone_numbers = [fake.phone_number() for _ in range(N)]
    fake_df = pd.DataFrame({'Name': names, 'Address': addresses, 'Email': emails, 'Phone Number': phone_numbers})
    return fake_df

    fake_users = create_fake_data(100)
    fake_users.head()

def main():
    '''x = np.linspace(0.1, 4, 50)

    j1 = np.sin(x) /x + np.cos(x) / x**2
    
    

    plt.plot(x, j1, label='j1(x)', color='blue')
    plt.title('Bessel Function of the First Kind (j1)')
    plt.xlabel('x')
    plt.ylabel('j1(x)') 
    plt.grid()
    plt.legend()
    plt.show()


    u,v = create_data(200, [2, 1])
    plt.figure(figsize=(10, 6))
    plt.title('Simulated Linear Data')  
    plt.xlabel('X')
    plt.ylabel('y')
    plt.scatter(u, v)
    plt.show()
    

    h, y = create_time_series(100, [0.25, 0.2])
    plt.figure(figsize=(10, 6))
    plt.title('Simulated Time Series Data')
    plt.xlabel('Time')
    plt.ylabel('y')
    plt.plot(h, y)
    plt.show()

    #project as a peace of code is getting better and better, but then he dosen't achieve the goal, this is really bad.
    #better you know the tecqunical details, then you can use ai
'''


    '''
    Clone your remote repository
    configure your git credentials
    setup your upstrem repository (point to my repository like a fork)


    Exam: first part CODING

    '''
    #brownian motion simulation
    N = 1000  # number of steps
    x = np.zeros(N)
    for i in range(1, N):
        x[i] = x[i-1] + np.random.normal(0, 1)  # random step

    sigma = np.std(x)
    plt.figure(figsize=(10, 6))
    plt.title('Brownian Motion Simulation')
    plt.xlabel('Steps')
    plt.ylabel('Position')  
    plt.plot(x, label='Brownian Motion', color='blue')
    plt.axhline(y=sigma, color='r', linestyle='--', label='Standard Deviation')
    plt.axhline(y=-sigma, color='r', linestyle='--', label='Negative Standard Deviation')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()