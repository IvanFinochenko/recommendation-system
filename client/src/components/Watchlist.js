import React from 'react';
import ReactPaginate from 'react-paginate';
import Header from './Header';
import MoviesList from './MoviesList';
import config from '../config';

export default class Watchlist extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			movies: [],
			pageCount: 0,
			currentPage: 0
		}
	}

	componentDidMount() {
		const params = { page: 0 }
		const url = new URL(config.server + "/api/watchlist");
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
			.then(data => this.setState({ movies: data.movies, pageCount: data.count_page}));	
	}

	handlePageClick(x) {
		const params = { page: x.selected + 1 }
		const url = new URL(config.server + "/api/watchlist");
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
				pageCount: data.count_page, 
				currentPage: x.selected}));
	}

	redirectLogout() {
		this.props.history.push("/");
	}

	render() {
		window.scrollTo(0,0);
		let paginate = null;
		if (this.state.pageCount > 1) {
			paginate = (
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
                </div>);
		}
		return (
			<div>
				<Header username={ localStorage.getItem("username")} redirect={ this.redirectLogout.bind(this) }/>
				{ paginate }
				<MoviesList movies={ this.state.movies }/>
				{ paginate }
			</div>
		);
	}
}