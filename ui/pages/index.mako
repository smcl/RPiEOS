<div class="jumbotron">
	<h1>
		Index
	</h2>
	<p>
		This is the main page of a very simple site.
	</p>
	<p>
		Here are some widgets loaded from an sqlite3 DB:
		<ul>
			% for widget in model:
				<li> 
					<b> ${widget[1]} </b> = ${widget[2]}
				</li>
			% endfor
		</ul>
	</p>	
</div>