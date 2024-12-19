import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Shop from "./components/Shop";
import Cart from "./components/Cart";
import Navbar from "./components/Navbar";
import { Bounce, ToastContainer } from "react-toastify";
import { Checkout } from "./components/Checkout";
import Orders from "./components/Orders";

export default function AppRouter() {
  return (
    <Router>
      <div>
        <ToastContainer
          position="bottom-center"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark"
          transition={Bounce}
        />
        <Routes>
          <Route
            path="/"
            element={
              <div>
                <Navbar />
                <Shop />
              </div>
            }
          />
          <Route
            path="/cart"
            element={
              <div>
                <Navbar />
                <Cart />
              </div>
            }
          />
          <Route
            path="/orders"
            element={
              <div>
                <Navbar />
                <Orders />
              </div>
            }
          />
          <Route
            path="/checkout"
            element={
              <div>
                <Navbar />
                <Checkout />
              </div>
            }
          />
          <Route path="*" element={<h1>404 Not Found</h1>} />
        </Routes>
      </div>
    </Router>
  );
}
