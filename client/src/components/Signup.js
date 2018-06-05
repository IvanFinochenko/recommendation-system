import React from 'react';
import { Form, FormGroup, Col, FormControl, Button, ControlLabel } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap';
import Header from './Header';
import './css/Signup.css';
import axios from 'axios';
import config from '../config';

class Signup extends React.Component {
	constructor(props) {
    	super(props);

    	this.state = {
      		username: "",
      		password1: "",
      		password2: "",
      		error: false
    	};
  	}

  	validateForm() {
    	return this.state.username.length > 0 && this.state.password1.length > 0 && this.state.password1 === this.state.password2;
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
  			password: this.state.password1
  		};
    	fetch(config.server + "/api/signup", {
			method: 'POST',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		},
    		body: JSON.stringify(credentials)
		})
    		.then(response => {
    			if (response.status == 200) {
    				return response.json();
    			} else {
    				this.setState({
    					username: "",
      					password1: "",
      					password2: "",
      					error: true
    				});
    			}
    		})
    		.then(data => {
    			localStorage.setItem("token", data.id); 
    			localStorage.setItem("username", data.username);
    			this.props.history.push("/");
    		})
  	}

	render() {
		let errorMessage = null;
		if (this.state.error) {
			errorMessage = (<div className="error_message_signup">Такой пользователь уже зарегистрирован</div>)
		} 
		return (
			<div>
				<Header />
				<Form horizontal onSubmit={ this.handleSubmit } className="Signup">
					{ errorMessage }
	  				<FormGroup controlId="username">
	    				<Col componentClass={ControlLabel} sm={3}>
	      					Логин
	    				</Col>
	    				<Col sm={9}>
	      					<FormControl 
	      						type="text" 
	      						placeholder="" 
	      						value={this.state.username} 
	      						onChange={this.handleChange} />
	    				</Col>
	  				</FormGroup>

	  				<FormGroup controlId="password1">
	   					 <Col componentClass={ControlLabel} sm={3}>
	      					Пароль
	    				</Col>
	    				<Col sm={9}>
	      					<FormControl 
	      						type="password" 
	      						placeholder="" 
	      						value={this.state.password1}
	              				onChange={this.handleChange} />
	    				</Col>
	  				</FormGroup>

	  				<FormGroup controlId="password2">
	   					 <Col componentClass={ControlLabel} sm={3}>
	      					Повторите пароль
	    				</Col>
	    				<Col sm={9}>
	      					<FormControl 
	      						type="password" 
	      						placeholder="" 
	      						value={this.state.password2}
	              				onChange={this.handleChange} />
	    				</Col>
	  				</FormGroup>

	 				<FormGroup>
	    				<Col smOffset={3} sm={9}>
	      					<Button type="submit" disabled={!this.validateForm()}>
	      						Зарегистрироваться
	      					</Button>
	    				</Col>
	  				</FormGroup>
				</Form>
			</div>
		);
	}
}

export default Signup