import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

class Doc extends React.Component {
  render() {
    return (
      <App />
    )
  }

  componentDidMount() {
    document.title = "Uncle Dunk | Dashboard"
  }
}


ReactDOM.render(
  <Doc />,
  document.getElementById('root')
);