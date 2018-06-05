import React from 'react';
import Select from 'react-select';
import axios from 'axios';
import 'react-select/dist/react-select.css';
import { Form, FormGroup, Col, FormControl, Button} from 'react-bootstrap';
import config from '../config';
import './css/Search.css';

export default class Search extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			selectedGenre: { value: -1, label: 'Все жанры' },
			selectedOption: { value: 1, label: 'Название' },
			searchText: "", 
			optionsGenre: []
		}
	}

	componentDidMount() {
		fetch(config.server + "/api/genres", {
			method: 'GET',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		}
		})
			.then(response => response.json())
			.then(data => { 
				this.setState({ optionsGenre: [{ value: -1, label: 'Все жанры' }, ...data.genres]});
			});
	}

	handleChange = (event) => {
    	this.setState({
      		searchText: event.target.value
    	});
  	}

  	handleChangeType = (selectedOption) => {
  		this.setState({ selectedOption });
  	}

  	handleSubmit() {
  		this.props.handleGenre({ 
  			genre_id: this.state.selectedGenre.value,
  			type_search: this.state.selectedOption.value,
  			text_search: this.state.searchText
  		});
  	}

  	handleChangeGenre = (selectedGenre) => {
  		this.setState({ selectedGenre });
  		this.props.handleGenre({ genre_id: selectedGenre.value, type_search: 1, text_search: "" });
  	}

  	validateForm() {
    	return this.state.searchText.length > 0;
  	}

	render() {
		return (
			<div className="search">
				<Select
					className="search__genre"
	        		name="form-field-name"
	        		placeholder="Жанр"
	        		value={ this.state.selectedGenre }
	        		onChange={ this.handleChangeGenre }
	        		options={ this.state.optionsGenre } />
				<Select
					className="search__type"
	        		name="form-field-name"
	        		placeholder=""
	        		value={this.state.selectedOption}
	        		onChange={this.handleChangeType}
	        		options={[
	          			{ value: 1, label: 'Название' },
	          			{ value: 2, label: 'Режиссёр' },
	          			{ value: 3, label: 'Страна' }
	        		]} />
		  		<input className="search__text" type="text" value={ this.state.searchText } onChange={ this.handleChange }/>
		  		<Button type="buttton" onClick={ this.handleSubmit.bind(this) }>
		      		Поиск
		      	</Button>
	  		</div>
		);
	}
}