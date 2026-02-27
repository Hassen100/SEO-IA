import { Component, Input } from '@angular/core';
import { Game } from '../../models/game';
import { CartService } from '../../services/cart';

@Component({
  selector: 'app-game-card',
  standalone: false,
  templateUrl: './game-card.html',
  styleUrl: './game-card.css',
})
export class GameCard {
  @Input() game!: Game;

  constructor(private cartService: CartService) {}

  addToCart(): void {
    this.cartService.addToCart(this.game);
  }
}
