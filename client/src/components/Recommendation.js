import React from 'react';
import Header from './Header';
import MoviesList from './MoviesList';
import config from '../config';
import './css/Recommendation.css';

export default class Recommendation extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			movies: [],
			notRatings: false
		}
	}

	getRecommendation() {
		fetch(config.server + "/api/recommendations", {
			method: 'GET',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		}
		})
			.then(response => { if (response.status == 200) {
					return response.json();
				} else {
					this.setState({ notRatings: true });
				}
			})
			.then(data => this.setState({ movies: data.movies }));
	}

	componentDidMount() {
		this.getRecommendation();
	}

	redirectLogout() {
		this.props.history.push("/");
	}

	render() {
		let recommendations = null;
		if (this.state.notRatings) {
			recommendations = (
				<h2 className="ratings__message" align="center">
					Для получения рекомендаций, оцените 10 фильмов
				</h2>
			);
		} else {
			recommendations = (
				<MoviesList movies={ this.state.movies } getRecommendation={ this.getRecommendation.bind(this) }/>
			);
		}
		return	(
			<div>
				<Header username={ localStorage.getItem("username")} redirect={ this.redirectLogout.bind(this) }/>
				{ recommendations }
			</div>
		);
	}
}