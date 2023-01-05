import React from "react";
import TextField from '@mui/material/TextField';

const Home = () => {
	return (
		<>
			<header class="header">
				<h1>Home</h1>
			</header>
			<article class="article">
				<section class="section">
					<h2>test</h2>
					<TextField id="ph" label="pH (-)" variant="standard" />
					<TextField id="ec" label="EC (µS/cm)" variant="standard" />
					<TextField id="tur" label="Turbidity (NTU)" variant="standard" />
				</section>
				<section class="section">
					This is some text 2
				</section>
				<section class="section">
					This is some loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong text 3
				</section>
				<section class="section">
					This is some loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong text 4
				</section>
			</article>
			<footer class="footer">
				Data Output!
			</footer>
		</>
	);
};

export default Home;
