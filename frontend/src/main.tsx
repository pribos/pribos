import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import Home from './pages/Home';
import Calendar from './pages/Calendar';
import Mailbox from './pages/Mailbox';
import './index.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route path="home" element={<Home />} />
          <Route path="calandar" element={<Calendar />} />
          <Route path="mailbox" element={<Mailbox />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
