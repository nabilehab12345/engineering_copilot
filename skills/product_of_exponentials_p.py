To solve the problem of finding the product of exponentials (PoE) formula in spatial robot kinematics using screw theory, we need to understand the core concepts and apply them in Python. The PoE formula is a mathematical representation of the transformation of a spatial frame from one configuration to another using a sequence of exponential maps.

Screw theory provides a compact and efficient way to represent rigid body motions. The exponential map in screw theory relates a twist (a combination of rotational and translational velocities) to a rigid body transformation.

The formula for the product of exponentials (PoE) is given by:
\[ T = \exp(\sum_{i=1}^{n} \mathbf{S}_i \theta_i) \]
where \( T \) is the resulting transformation, \( \mathbf{S}_i \) are the screws ( twists), and \( \theta_i \) are the parameters (angles or time intervals).

Here is a Python function that implements this formula using NumPy for numerical computations:

```python
import numpy as np

def exponential_map(screw, theta):
    """
    Compute the exponential map of a screw (twist).
    
    Args:
        screw (np.array): A 6x1 array representing the screw (twist).
        theta (float): The parameter (angle or time interval).
        
    Returns:
        np.array: A 4x4 transformation matrix.
    """
    w = screw[:3]  # rotational part
    v = screw[3:]  # translational part
    w_norm = np.linalg.norm(w)
    
    if w_norm == 0:
        # Pure translation
        R = np.eye(3)
        V = np.array([
            [0, -v[2], v[1]],
            [v[2], 0, -v[0]],
            [-v[1], v[0], 0]
        ])
        return np.eye(4) + theta * V + (theta**2 / 2) * V @ V
    
    # Rotational part
    R = np.eye(3)
    W = np.array([
        [0, -w[2], w[1]],
        [w[2], 0, -w[0]],
        [-w[1], w[0], 0]
    ])
    R = np.eye(3) + np.sin(w_norm * theta) / w_norm * W + (1 - np.cos(w_norm * theta)) / (w_norm ** 2) * W @ W
    
    # Translation part
    V = np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = v * theta + (np.sin(w_norm * theta) / w_norm - 1) * (R @ v)
    
    return T

def product_of_exponentials(screws, thetas):
    """
    Compute the product of exponentials (PoE) of a sequence of screws.
    
    Args:
        screws (list of np.array): A list of 6x1 arrays representing the screws (twists).
        thetas (list of float): A list of parameters (angles or time intervals).
        
    Returns:
        np.array: A 4x4 transformation matrix.
    """
    T = np.eye(4)
    for screw, theta in zip(screws, thetas):
        T = T @ exponential_map(screw, theta)
    return T

# Example usage
screws = [
    np.array([0, 0, 1, 1, 0, 0]),  # Screw (twist) 1
    np.array([1, 0, 0, 0, 1, 0])   # Screw (twist) 2
]
thetas = [np.pi / 2, np.pi / 4]    # Parameters (angles)

T = product_of_exponentials(screws, thetas)
print("Transformation Matrix T:")
print(T)
```

### Explanation:
1. **Exponential Map Function (`exponential_map`)**:
   - Computes the exponential map for a single screw (twist) and parameter.
   - Handles both pure translation and general screw transformations.

2. **Product of Exponentials Function (`product_of_exponentials`)**:
   - Iterates through a list of screws and their corresponding parameters, computing the exponential map for each and multiplying the resulting transformation matrices.

### Example Usage:
- Define a list of screws and their corresponding parameters.
- Call the `product_of_exponentials` function to compute the overall transformation matrix.

This function is reusable and can be applied to any sequence of screws and parameters to compute the resulting transformation matrix in spatial robot kinematics.