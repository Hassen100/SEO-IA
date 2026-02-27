import { Injectable } from '@angular/core';
import { Game } from '../models/game';

export interface CartItem {
  game: Game;
  quantity: number;
}

@Injectable({
  providedIn: 'root',
})
export class CartService {
  private items: CartItem[] = [];

  addToCart(game: Game): void {
    const existingItem = this.items.find(item => item.game.id === game.id);
    if (existingItem) {
      existingItem.quantity++;
    } else {
      this.items.push({ game, quantity: 1 });
    }
  }

  removeFromCart(gameId: number): void {
    this.items = this.items.filter(item => item.game.id !== gameId);
  }

  getItems(): CartItem[] {
    return this.items;
  }

  getTotalItems(): number {
    return this.items.reduce((total, item) => total + item.quantity, 0);
  }

  getTotalPrice(): number {
    return this.items.reduce((total, item) => total + (item.game.price * item.quantity), 0);
  }

  clearCart(): void {
    this.items = [];
  }
}
