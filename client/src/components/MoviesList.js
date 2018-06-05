import React from 'react';
import axios from 'axios';
import Movie from './Movie';
import config from '../config';
import { Table } from 'react-bootstrap';
import './css/MoviesList.css';

class MoviesList extends React.Component {
	constructor(props) {
		super(props)
	}

	render() {
		const movies = this.props.movies;
		let tableMovies = [];
		for (var i = 0; i < movies.length - 1; i += 2) {
			tableMovies = [...tableMovies, (
				<tr key={movies[i].id}>
					<td className="col__left">
						<Movie 
							id={ movies[i].id }
							title={ movies[i].title }
							year={ movies[i].year } 
							country={ movies[i].country } 
							rating={ movies[i].rating } 
							poster={ movies[i].poster_url }
							vote={ movies[i].vote }
							getRecommendation={ this.props.getRecommendation }
							isWatchlist={ movies[i].isWatchlist }/>
					</td>
					<td className="col__right">
						<Movie
							id={ movies[i + 1].id }
							title={ movies[i + 1].title }
							year={ movies[i + 1].year } 
							country={ movies[i + 1].country } 
							rating={ movies[i + 1].rating } 
							poster={ movies[i + 1].poster_url }
							vote={ movies[i + 1].vote }
							getRecommendation={ this.props.getRecommendation }
							isWatchlist={ movies[i].isWatchlist }/>
					</td>
				</tr>
			)];
		}
		if (movies.length % 2 == 1) {
			const i = movies.length - 1
			tableMovies = [...tableMovies, (
				<tr key={movies[i].id}>
					<td className="col__left">
						<Movie 
							id={ movies[i].id }
							title={ movies[i].title }
							year={ movies[i].year } 
							country={ movies[i].country } 
							rating={ movies[i].rating } 
							poster={ movies[i].poster_url }
							vote={ movies[i].vote }
							getRecommendation={ this.props.getRecommendation }
							isWatchlist={ movies[i].isWatchlist }/>
					</td>
				</tr>
			)];
		} 
		return (
			<div>
				<Table>
					<tbody>
						{ tableMovies }
					</tbody>
				</Table>
					
			</div>
		);
	}
}

export default MoviesList;