import { Route, RouteHandler, Link } from 'react-router';
import { Label, Nav, Navbar, NavItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import axios from 'axios';
import React from 'react';
import config from '../config';
import './css/Header.css';

export default class Header extends React.Component {
	constructor(props){
		super(props);
	}

	handleLogout() {
		fetch(config.server + "/api/logout", {
			method: 'GET',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		}
		})
			.then(response => response.json())
			.then(data => { 
				localStorage.removeItem("username");
				localStorage.removeItem("token");
				this.props.redirect();
			});
	}

	render() {
		return (
			<Navbar inverse collapseOnSelect>
				<Nav>
					<LinkContainer to="/movies">
						<NavItem eventKey={1}>Фильмы</NavItem>
					</LinkContainer>
					<LinkContainer to="/recommendation">
						<NavItem eventKey={2}>Рекомендации</NavItem>
					</LinkContainer>
					<LinkContainer to="/watchlist">
						<NavItem eventKey={3}>Буду смотреть</NavItem>
					</LinkContainer>
				</Nav>
				{ this.props.username ? (
					<Nav pullRight className="logout">
						<h4 className="logout__username">
						<Label>
							{ this.props.username }
						</Label>
						</h4>
						<LinkContainer to="/signin">
							<NavItem eventKey={1} className="logout__button" onClick={ this.handleLogout }>Выйти</NavItem>
						</LinkContainer>
					</Nav>		
				) : (
					<Nav pullRight>
						<LinkContainer to="/signin">
							<NavItem eventKey={1}>Войти</NavItem>
						</LinkContainer>
					</Nav>
				)}
			</Navbar>
		);
	}
}