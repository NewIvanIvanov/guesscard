(function() {

values = {
	cardsBox: "#cards_box",
	cardsNumber: 12,
	csrfSelector: "#ModalCenter input[name=csrfmiddlewaretoken]",
	url: "/getscore/",
};

values.cardsNumber = cardsNumberFromUser;

function DeckOfCards(cardsNumber, cardsBox) {
	self = this;
	this.arrayOfCards = [];
	this.openCardsCounter = 0;
	this.firstOpenedCard = undefined;
	this.secondOpenedCard = undefined;
	this.movesCounter = 0;
	this.cardsNumber = cardsNumber;
	this.cardsBox = cardsBox;
	this.cardsLeft = cardsNumber;

	DeckOfCards.prototype.dealTheCards = function() {
		$(cardsBox).innerHTML = '';
		for (var i = 0; i < self.cardsNumber; i++) {
			$(self.cardsBox).append(
				'<div class="card_image">' + 
					'<div id="card_back_side_' + i + '" class="card"></div>' +
				'</div>');
		}
	};


	DeckOfCards.prototype.shuffleCards = function() {
		var i, j, x;
		self.arrayOfCards = [];
		for (var n = 0; n < self.cardsNumber / 2; n++) {
			self.arrayOfCards.push(n, n);
		}
		
		for (i = self.cardsNumber - 1; i > 0; i--) {
			j = Math.floor(Math.random() * (i + 1));
			x = self.arrayOfCards[i];
			self.arrayOfCards[i] = self.arrayOfCards[j];
			self.arrayOfCards[j] = x;
		}
	};


	DeckOfCards.prototype.clickOnCardHandler = function(event) {
		if (event.target.id.slice(0,15) == 'card_back_side_') {

			if (self.openCardsCounter === 0) {
				self.openCardsCounter++;
				self.firstOpenedCard = event.target;
				self.showCardOnClick(self.firstOpenedCard, event);
			}

			if (self.openCardsCounter === 1 && event.target !== self.firstOpenedCard) {
				self.openCardsCounter++;
				self.movesCounter++;
				self.secondOpenedCard = event.target;
				self.showCardOnClick(self.secondOpenedCard, event);

				if(self.cardsAreGuessed(self.firstOpenedCard, self.secondOpenedCard, event)) {
					self.cardsLeft -= 2;
					setTimeout(function() {
							self.clearTwoCardsOnSuccess();
							self.resetChosenCards();
							self.checkForWin();
						}, 300);
				} else {

					setTimeout(function() {
						self.firstOpenedCard.style.visibility = 'visible';
						self.secondOpenedCard.style.visibility = 'visible';
						self.resetChosenCards();
					}, 1000);
				}

				$("#moves_counter").text('Your\'s turn: ' + self.movesCounter);
			}


		}
	};


	DeckOfCards.prototype.addClick = function() {
		$(self.cardsBox).click(self.clickOnCardHandler);
	};

	DeckOfCards.prototype.cardsAreGuessed = function(firstCard, secondCard) {
		return self.arrayOfCards[firstCard.id.slice(15)] === self.arrayOfCards[secondCard.id.slice(15)];
	};

	DeckOfCards.prototype.showCardOnClick = function(card, event) {
		self.setCardBackgroundImage(card, event);
		event.target.style.opacity = 0;
		setTimeout(function() {
			event.target.style.visibility = 'hidden';
		}, 300);
	};

	DeckOfCards.prototype.resetChosenCards = function() {
		self.openCardsCounter = 0;
		self.firstOpenedCard.style.opacity = 1;
		self.secondOpenedCard.style.opacity = 1;
		self.firstOpenedCard = undefined;
		self.secondOpenedCard = undefined;

	};

	DeckOfCards.prototype.getCardNumber = function(event) {
		return self.arrayOfCards[event.target.id.slice(15)];
	};

	DeckOfCards.prototype.setCardBackgroundImage = function(card, event) {
		if (card.parentNode.style.backgroundImage === "") {
			card.parentNode.style.backgroundImage = 
			"url('/static/guess_two_cards/img/card_" + self.getCardNumber(event) + ".png')";
		}
	};

	DeckOfCards.prototype.clearTwoCardsOnSuccess = function() {
		self.firstOpenedCard.parentNode.style.opacity = 0;
		self.secondOpenedCard.parentNode.style.opacity = 0;
	};

	DeckOfCards.prototype.run = function() {
		self.shuffleCards();
		self.dealTheCards();
		self.addClick();
	};

	DeckOfCards.prototype.checkForWin = function() {
		if (self.cardsLeft === 0) {
			$('#ModalCenter').modal('show');
			$('#modal-text').text('Your score is ' + self.movesCounter + ' turns.');
			var dataTransfer = new DataTransfer(values.url, values.csrfSelector, self.movesCounter, self.cardsNumber);
			dataTransfer.run();
		}
	};
}

function DataTransfer(dataUrl, csrfSelector, score, cardsNumber) {
	this.dataUrl = dataUrl;
	this.csrfToken = $(csrfSelector).val();
	self = this;


	DataTransfer.prototype.prepareData = function() {
		var formData = new FormData();
		formData.append("csrfmiddlewaretoken", this.csrfToken);
		formData.append("score", score);
		formData.append("cardsNumber", cardsNumber);
		return formData;
	};

	DataTransfer.prototype.sendData = function(data) {
		var xml = new XMLHttpRequest();
		xml.open("POST", dataUrl);

	    xml.onload = function() {
	      if (xml.status === 200) {
	        var response = JSON.parse(xml.responseText); 
	        console.log(response);
	      }
	    };

	    xml.onerror = function() {
	    	console.log("Send data error.");
	    };

    xml.send(data);
	};

	DataTransfer.prototype.run = function() {
		var data = self.prepareData();
		self.sendData(data);
	};
	
}

newDeck = new DeckOfCards(values.cardsNumber, values.cardsBox);
newDeck.run();
})();

