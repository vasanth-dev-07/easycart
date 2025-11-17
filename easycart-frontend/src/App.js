import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Register from './components/Register';
import Signin from './components/Signin';
import Showcart from './components/Showcart';
import ProductList from './components/ProductList';

// {/* <Route path="/products" element={<ProductList />} /> */}



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/products" element={<ProductList />} />
        <Route path="/showcart" element={<Showcart />} />
        {/* <Route path="/logout" element={<Signout />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
