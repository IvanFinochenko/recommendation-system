import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Movies from './Movies';
import Signin from './Signin';
import Signup from './Signup';
import MovieDescription from './MovieDescription';
import Recommendation from './Recommendation';
import Watchlist from './Watchlist';

export default () => {
	return (
		<Router>
			<div>
				<Route exact path='/' component={ Movies } />
    			<Route path='/movies' component={ Movies } />
    			<Route path='/signin' component={ Signin } />
    			<Route path='/signup' component={ Signup } />
    			<Route path='/movie/:id' component={ MovieDescription } />
                <Route path='/recommendation' component={ Recommendation } />
                <Route path='/watchlist' component={ Watchlist } />
    		</div>
    	</Router>
	);
}