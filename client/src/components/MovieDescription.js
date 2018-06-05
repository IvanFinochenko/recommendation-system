import React from 'react';
import { Table } from 'react-bootstrap';
import axios from 'axios';
import StarRatingComponent from 'react-star-rating-component';
import config from '../config';
import Header from './Header';
import './css/MovieDescription.css';

export default class MovieDescription extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			movie: {},
			fields: [
				"Год",
				"Страна",
				"Режиссёр",
				"Продолжительность",
				"Жанр",
				"Бюджет",
				"Сборы",
				"Возраст",
				"Изображение"
			]
		};
	}

	componentDidMount() {
		fetch(config.server + "/api/movie/" + this.props.match.params.id, {
			method: 'GET',
			credentials: 'include',
    		headers: {
    			Accept: 'application/json',
    			'Content-Type': 'application/json',
    		}
		})
			.then(response => response.json())
			.then(data => {
				console.log(data)
				this.setState({ movie: data });
			});
	}

	render() {
		const movieDesc = [
			this.state.movie.year,
			this.state.movie.country,
			this.state.movie.director,
			this.state.movie.runtime,
			this.state.movie.genres,
			this.state.movie.budget,
			this.state.movie.box_office,
			this.state.movie.age,
			this.state.movie.image
		];
		let rows = [];
		for (var i = 0; i < this.state.fields.length; i++) {
			rows = [...rows, (
				<tr style={{fontSize: 20}}>
					<td>
						{ this.state.fields[i] }
					</td>
					<td>
						{ movieDesc[i] }
					</td>
				</tr>
			)];			
		}
		return (
			<div>
				<Header />
				<div className="description">
					<img 
						className="description__image" 
						src={this.state.movie.poster_url ? this.state.movie.poster_url : "http://tonnakino.me/uploads/posts/2016-07/1468836798_uet.jpg"}/>
					<div className="description__info">
						<h1>{ this.state.movie.title }</h1>
						<h4>Оценка:</h4>
						<div style={{fontSize: 30}}>
							<StarRatingComponent
								name="rating"
								starCount={10}
		          				value={ this.state.movie.rating }
		          				editing={false}
							/>
						</div>
						<h4>Твоя оценка:</h4>
						<div style={{fontSize: 30}}>
							<StarRatingComponent
								name="rate"
								starCount={10}
		          				value={ this.state.movie.vote }
		          				onStarClick={this.onStarClick}
							/>
						</div>
						<Table>
							<tbody>
								{ rows }
							</tbody>
						</Table>
					</div>
				</div>
			</div>
		);
	}
}