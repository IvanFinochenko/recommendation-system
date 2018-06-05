import React from 'react';
import { Form, FormGroup, Col, FormControl, Button, ControlLabel } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import axios from 'axios';
import Header from './Header';
import './css/Signin.css';
import config from '../config';

class Signin extends React.Component {
	constructor(props) {
    	super(props);

    	this.state = {
      		username: "",
      		password: "",
      		error: false
    	};
  	}

  	validateForm() {
    	return this.state.username.length > 0 && this.state.password.length > 0;
  	}

  	handleChange = event => {
    	this.setState({
      		[event.target.id]: event.target.value
    	});
  	}

  	handleSubmit = event => {
    	event.preventDefault();
    	const credentials = {
    		username: this.state.username,
    		password: this.state.password
    	};

    	fetch(config.server + "/api/login", {
			method: 'POST',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		},
    		body: JSON.stringify(credentials)
		})
			.then(response => {	if (response.status == 200) {
					return response.json();
				} else {
						this.setState({
    					username: "",
    					password: "",
    					error: true
    				});
				}
			})
			.then(data => {
				localStorage.setItem("token", data.id); 
    			localStorage.setItem("username", data.username);
    			this.props.history.push("/");
    		})
    		.catch(error => {
    			this.setState({
    				username: "",
    				password: "",
    				error: true
    			});
    		});
  	}

	render () {
		let errorMessage = null;
		if (this.state.error) {
			errorMessage = (<div className="error_message">Неправильный логин или пароль</div>)
		}
		return (
			<div>
				<Header />
				<Form horizontal onSubmit={ this.handleSubmit } className="Signin">
					{ errorMessage }
	  				<FormGroup controlId="username">
	    				<Col componentClass={ControlLabel} sm={2}>
	      					Логин
	    				</Col>
	    				<Col sm={10}>
	      					<FormControl 
	      						type="text" 
	      						placeholder="" 
	      						value={this.state.username} 
	      						onChange={this.handleChange} />
	    				</Col>
	  				</FormGroup>

	  				<FormGroup controlId="password">
	   					 <Col componentClass={ControlLabel} sm={2}>
	      					Пароль
	    				</Col>
	    				<Col sm={10}>
	      					<FormControl 
	      						type="password" 
	      						placeholder="" 
	      						value={this.state.password}
	              				onChange={this.handleChange} />
	    				</Col>
	  				</FormGroup>

	 				<FormGroup>
	    				<Col smOffset={2} sm={10}>
	      					<Button 
	      						type="submit"
	            				disabled={!this.validateForm()}
	      					>
	      						Войти
	      					</Button>
	    				</Col>
	  				</FormGroup>
	  				<FormGroup>
	    				<Col smOffset={2} sm={10}>
	    					<LinkContainer to='/signup'>
	      						<Button>
	      							Зарегистрироваться
	      						</Button>
	      					</LinkContainer>
	    				</Col>
	  				</FormGroup>
				</Form>
			</div>
		);
	}
}

export default Signin