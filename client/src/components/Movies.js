import React from 'react';
import ReactPaginate from 'react-paginate';
import Header from './Header';
import { LinkContainer } from 'react-router-bootstrap';
import MoviesList from './MoviesList';
import axios from 'axios';
import config from '../config';
import Search from './Search';
import './css/Movies.css';

export default class Movies extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentPage: 0,
			pageCount: 40,
			movies: [],
			genre_id: -1,
			text_search: "",
			type_search: 1
		};
	}

	redirectLogout() {
		this.props.history.push("/");
	}

	fetch() {
		fetch(config.server + "/api/movies/1", {
			method: 'GET',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		}
		})
			.then(response => response.json())
			.then(data => this.setState({ movies: data.movies, pageCount: data.count_page}));		
	}

	componentDidMount() {
		this.fetch();
		console.log(localStorage.getItem("token"));
	}

	handlePageClick(x) {
		const params = {
			genre_id: this.state.genre_id, 
		 	type_search: this.state.type_search, 
		 	text_search: this.state.text_search
		};
		const url = new URL(config.server + "/api/movies/" + (x.selected + 1));
		Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
		fetch(url, {
			method: 'GET',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		}
		})
			.then(response => response.json())
			.then(data => this.setState({ 
				movies: data.movies, 
				currentPage: x.selected, 
				pageCount: data.count_page
			}));
	} 

	handleGenre(params) {
		const url = new URL(config.server + "/api/movies/1");
		Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
		fetch(url, {
			method: 'GET',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		}
		})
			.then(response => response.json())
			.then(data => this.setState({ 
				movies: data.movies,
				currentPage: 0,
				genre_id: params.genre_id,
				type_search: params.type_search,
				text_search: params.text_search,
				pageCount: data.count_page
			}));
	}

	render() {
		window.scrollTo(0,0);
		return (
			<div>
				<Header username={ localStorage.getItem("username")} redirect={ this.redirectLogout.bind(this) }/>
				<Search handleGenre={ this.handleGenre.bind(this) } />
				<div className="movie__paginate">
					<ReactPaginate
						previousLabel={"<"}
		                nextLabel={">"}
		                breakLabel={<a href="">...</a>}
		                breakClassName={"break-me"}
		                pageCount={this.state.pageCount}
		                marginPagesDisplayed={2}
		                pageRangeDisplayed={5}
		                onPageChange={this.handlePageClick.bind(this)}
		                containerClassName={"pagination"}
		                subContainerClassName={"pages pagination"}
	                    activeClassName={"active"}
	                    forcePage={ this.state.currentPage } />
                </div>
				<MoviesList movies={ this.state.movies }/>
				<div className="movie__paginate">
					<ReactPaginate
						previousLabel={"<"}
		                nextLabel={">"}
		                breakLabel={<a href="">...</a>}
		                breakClassName={"break-me"}
		                pageCount={this.state.pageCount}
		                marginPagesDisplayed={2}
		                pageRangeDisplayed={5}
		                onPageChange={this.handlePageClick.bind(this)}
		                containerClassName={"pagination"}
		                subContainerClassName={"pages pagination"}
	                    activeClassName={"active"}
	                    forcePage={ this.state.currentPage } />
                </div>
			</div>
		);
	}
}