import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // ✅ import navigate

function ProductList() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/products/products/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }
        return response.json();
      })
      .then(data => {
        setProducts(data);
        const initial = {};
        data.forEach(p => (initial[p.id] = 1));
        setQuantities(initial);
      })
      .catch(error => {
        console.error('Error:', error);
        setError('Failed to fetch products');
      });
  }, []);

  const increaseQuantity = (id, stock) => {
    setQuantities(prev => ({
      ...prev,
      [id]: Math.min(prev[id] + 1, stock),
    }));
  };

  const decreaseQuantity = (id) => {
    setQuantities(prev => ({
      ...prev,
      [id]: Math.max(prev[id] - 1, 1),
    }));
  };

  const handleAddToCart = async (productId) => {
    const token = localStorage.getItem('access');
    const quantity = quantities[productId];

    try {
      const response = await fetch('http://localhost:8000/orders/addcart/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ product: productId, quantity }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
      } else {
        setMessage(data.error || 'Failed to add to cart');
      }
    } catch (err) {
      console.error(err);
      setMessage('Something went wrong while adding to cart');
    }
  };

  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-5">
      {/* 🔘 Cart Button */}
      <div className="text-end mb-3">
        <button className="btn btn-success" onClick={() => navigate('/showcart')}>
        🧺 Show Cart
        </button>
      </div>

      <h2 className="text-center my-4 p-3 text-dark rounded shadow"
        style={{
          backgroundColor: '#d4edda',
          color: '#155724',
          fontWeight: 'bold',
          letterSpacing: '1px',
          fontSize: '2rem',
        }}
      >
        🛍️ Easy Cart
      </h2>

      {message && (
        <div className="alert alert-info text-center">{message}</div>
      )}

      <div className="row">
        {products.map(product => (
          <div className="col-md-4 mb-4" key={product.id}>
            <div className="card shadow-sm" style={{ fontSize: '0.9rem' }}>
              <img
                src={product.image}
                className="card-img-top"
                alt={product.name}
                style={{ height: '180px', objectFit: 'cover' }}
              />
              <div className="card-body p-3">
                <h5 className="card-title mb-2">{product.name}</h5>
                <p className="card-text">{product.description}</p>
                <p className="card-text"><strong>Price:</strong> ₹{product.price}</p>
                <p className="card-text"><strong>Stock:</strong> {product.stock}</p>

                <div className="d-flex align-items-center justify-content-center mb-2">
                  <button
                    className="btn btn-outline-secondary btn-sm"
                    onClick={() => decreaseQuantity(product.id)}
                  >−</button>

                  <input
                    type="text"
                    className="form-control text-center mx-2"
                    value={quantities[product.id]}
                    readOnly
                    style={{ width: '50px' }}
                  />

                  <button
                    className="btn btn-outline-secondary btn-sm"
                    onClick={() => increaseQuantity(product.id, product.stock)}
                  >+</button>
                </div>

                <button
                  className="btn btn-sm btn-primary w-100"
                  onClick={() => handleAddToCart(product.id)}
                >
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductList;
