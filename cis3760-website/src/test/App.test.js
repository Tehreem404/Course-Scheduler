import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
// import ReactDOM from 'react-dom';
window.React = React

import Header from '../components/Header.js';
import Footer from '../components/Footer.js';

describe('Header tests', () => {
    it('Contains proper text', () => {
	    render(<Header />);
        const heading = screen.getByText(/Course Catalog/i);
        expect(heading).toBeInTheDocument()
    });
});

describe('Footer tests', () => {
    it('Contains proper text', () => {
	    render(<Footer />);
        const heading = screen.getByText(/Course 3760 - Team 303/i);
        expect(heading).toBeInTheDocument()
    });
});
