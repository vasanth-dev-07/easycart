import React, { useEffect, useState } from 'react';

function Showcart() {
  const [cartItems, setCartItems] = useState([]);
  const [message, setMessage] = useState('');
  const [selectedItems, setSelectedItems] = useState([]);

  useEffect(() => {
    const fetchCart = async () => {
      const token = localStorage.getItem('access');
      if (!token) {
        setMessage('Please log in to view your cart');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/orders/viewcart/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setCartItems(data);
        } else {
          setMessage(data.error || 'Failed to fetch cart');
        }
      } catch (error) {
        console.error(error);
        setMessage('Something went wrong');
      }
    };

    fetchCart();
  }, []);

  const toggleSelect = (itemId) => {
    setSelectedItems(prev =>
      prev.includes(itemId)
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    );
  };

  const totalSelectedPrice = cartItems
    .filter(item => selectedItems.includes(item.id))
    .reduce((total, item) => total + parseFloat(item.total_price), 0);

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">🛒 Your Cart</h2>

      {message && <div className="alert alert-info text-center">{message}</div>}
      {cartItems.length === 0 && !message && <p className="text-center">Your cart is empty.</p>}

      <div className="row">
        {cartItems.map(item => (
          <div className="col-md-4 mb-4" key={item.id}>
            <div className="card shadow-sm">
              <img
                src={item.product.image}
                className="card-img-top"
                alt={item.product.name}
                style={{ height: '180px', objectFit: 'cover' }}
              />
              <div className="card-body">
                <h5 className="card-title">{item.product.name}</h5>
                <p className="card-text"><strong>Category:</strong> {item.product.category}</p>
                <p className="card-text"><strong>Price:</strong> ₹{item.product.price}</p>
                <p className="card-text"><strong>Quantity:</strong> {item.quantity}</p>
                <p className="card-text"><strong>Total:</strong> ₹{item.total_price}</p>
                <button
                  className={`btn btn-sm mt-2 ${selectedItems.includes(item.id) ? 'btn-danger' : 'btn-outline-primary'}`}
                  onClick={() => toggleSelect(item.id)}
                >
                  {selectedItems.includes(item.id) ? 'Unselect' : 'Select'}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedItems.length > 0 && (
        <div className="mt-4 text-center">
          <h5>Total Selected Price: ₹{totalSelectedPrice.toFixed(2)}</h5>
          <button className="btn btn-success me-2">Proceed to Checkout</button>
          <button className="btn btn-danger">Delete Selected</button>
        </div>
      )}
    </div>
  );
}

export default Showcart;
