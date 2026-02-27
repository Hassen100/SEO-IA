import { Component, Output, EventEmitter } from '@angular/core';
import { CartService } from '../../services/cart';

@Component({
  selector: 'app-header',
  standalone: false,
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header {
  totalItems = 0;
  @Output() cartToggle = new EventEmitter<void>();

  constructor(private cartService: CartService) {
    this.updateCartCount();
  }

  toggleCart(): void {
    this.cartToggle.emit();
    this.updateCartCount();
  }

  private updateCartCount(): void {
    this.totalItems = this.cartService.getTotalItems();
  }
}
