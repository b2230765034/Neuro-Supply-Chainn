import React from 'react'
import ReactDOM from 'react-dom/client'
// Dapp-kit based wallet providers are currently disabled per project decision
// If you want to re-enable wallet integration later, uncomment the imports and
// the provider wrapper below. Keep the dapp-kit package installed when used.
// import { SuiClientProvider, WalletProvider } from '@mysten/dapp-kit';
// import { getFullnodeUrl } from '@mysten/sui/client';
// import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
// import '@mysten/dapp-kit/dist/index.css';

import App from './App.jsx'
import './styles/App.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);