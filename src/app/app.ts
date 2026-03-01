import { Component, signal, ViewChild, AfterViewInit } from '@angular/core';
import { Game } from './models/game';
import { ShoppingCart } from './components/shopping-cart/shopping-cart';
import { CartService } from './services/cart';
import { Header } from './components/header/header';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  standalone: false,
  styleUrl: './app.css'
})
export class App implements AfterViewInit {
  protected readonly title = signal('magasin-jeux');
  @ViewChild('cart') cart!: ShoppingCart;
  @ViewChild('header') header!: Header;
  
  games: Game[] = [
    {
      id: 1,
      name: 'FIFA 2024',
      price: 69.99,
      image: 'https://picsum.photos/seed/fifa2024/300/200',
      description: 'Le meilleur jeu de football avec des graphiques ultra-réalistes'
    },
    {
      id: 2,
      name: 'Call of Duty Modern Warfare III',
      price: 79.99,
      image: 'https://picsum.photos/seed/codmw3/300/200',
      description: 'Action intense et multijoueur compétitif'
    },
    {
      id: 3,
      name: 'Grand Theft Auto VI',
      price: 89.99,
      image: 'https://picsum.photos/seed/gta6/300/200',
      description: 'Monde ouvert ultime avec une liberté totale'
    }
  ];

  constructor(private cartService: CartService) {}

  ngAfterViewInit(): void {
    // Mettre à jour le compteur du panier périodiquement
    setInterval(() => {
      if (this.header) {
        this.header.totalItems = this.cartService.getTotalItems();
      }
    }, 100);
  }

  openCart(): void {
    if (this.cart) {
      this.cart.openCart();
    }
  }

  scrollToJeux(): void {
    document.getElementById('jeux')?.scrollIntoView({ behavior: 'smooth' });
  }
}
