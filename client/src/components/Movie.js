import React from 'react';
import StarRatingComponent from 'react-star-rating-component';
import { LinkContainer } from 'react-router-bootstrap';
import { Button } from 'react-bootstrap';
import './css/Movie.css';
import config from '../config';

export default class Movie extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			i: 0,
			vote: null,
			isWatchlist: false,
			isDeleteMovie: false
		}
	}

	onStarClick(nextValue, prevValue, name) {
    	fetch(config.server + "/api/rating", {
			method: 'POST',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		},
    		body: JSON.stringify({
    			movie_id: this.props.id,
    			rating: nextValue
    		})
		})
			.then(response => {
				if (this.props.getRecommendation) {
					this.props.getRecommendation();
				} else {
					this.setState({ vote: nextValue });
				}
			});
  	}

  	handleWatchList() {
  		fetch(config.server + "/api/watchlist", {
			method: 'POST',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		},
    		body: JSON.stringify({
    			movie_id: this.props.id,
    		})
		})
			.then(response => {
				if (this.props.getRecommendation) {
					this.props.getRecommendation();
				} else {
					this.setState({ isWatchlist: true });
				}
			});
  	}

  	handleDeleteMovie() {
  		this.setState({
  			isDeleteMovie: true
  		})
  		fetch(config.server + "/api/watchlist", {
			method: 'DELETE',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		},
    		body: JSON.stringify({
    			movie_id: this.props.id,
    		})
		})
  	}

  	render() {
  		let add_watchlist = null;
  		let rating_user = null;
  		if (!this.props.vote) {
  			if (!this.state.vote 
  				&& localStorage.getItem("username") 
  				&& !this.props.isWatchlist 
  				&& !this.state.isWatchlist)
  				add_watchlist = (<Button onClick={ this.handleWatchList.bind(this) }>Буду смотреть</Button>);
  			if (localStorage.getItem("username")) {
  				rating_user = (
  					<div>
	  					<h4>Твоя оценка:</h4>
						<div style={{fontSize: 30}}>
		  					<StarRatingComponent
									name="rate"
									starCount={ 10 }
			          				value={ this.state.vote ? this.state.vote : this.props.vote }
			          				onStarClick={ this.onStarClick.bind(this) }/>
		          		</div>
	          		</div>
	          	);
	        }
	    } else {
	    	rating_user = (
		    	<div>
		  			<h4>Твоя оценка:</h4>
					<div style={{fontSize: 30}}>
			  			<StarRatingComponent
							name="rate"
							starCount={ 10 }
				          	value={ this.props.vote }/>
			          </div>
		        </div>
	        );
	    }
	    let deleteMovie = null;
	    if (this.props.isWatchlist && !this.state.isDeleteMovie) {
	    	deleteMovie = (<Button className="delete_movie" onClick={ this.handleDeleteMovie.bind(this) }>X</Button>)
	    }
		return (
			<div className='movie'>
				<img className='movie__image' src={this.props.poster ? this.props.poster : "http://tonnakino.me/uploads/posts/2016-07/1468836798_uet.jpg"}/>
				<div className='movie__info'>
					<div className="title">
						<LinkContainer to={ "/movie/" + this.props.id }>
							<a className="title__movie"><h2>{ this.props.title }</h2></a>
						</LinkContainer>
						{ deleteMovie }
					</div>
					<h4>Год: { this.props.year }</h4>
					<h4>Страна: { this.props.country }</h4>
					<h4>Оценка:</h4>
					<div style={{fontSize: 30}}>
						<StarRatingComponent
							name="rating"
							starCount={10}
	          				value={ this.props.rating }
	          				editing={false}
						/>
					</div>
					{ rating_user }
					{ add_watchlist }
				</div>
			</div>
		);
	}
}