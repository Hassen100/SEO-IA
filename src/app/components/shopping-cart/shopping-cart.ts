import { Component } from '@angular/core';
import { CartService, CartItem } from '../../services/cart';

@Component({
  selector: 'app-shopping-cart',
  standalone: false,
  templateUrl: './shopping-cart.html',
  styleUrl: './shopping-cart.css',
})
export class ShoppingCart {
  isOpen = false;
  items: CartItem[] = [];
  totalPrice = 0;

  constructor(private cartService: CartService) {}

  openCart(): void {
    this.isOpen = true;
    this.updateCart();
  }

  closeCart(): void {
    this.isOpen = false;
  }

  removeItem(gameId: number): void {
    this.cartService.removeFromCart(gameId);
    this.updateCart();
  }

  private updateCart(): void {
    this.items = this.cartService.getItems();
    this.totalPrice = this.cartService.getTotalPrice();
  }
}
