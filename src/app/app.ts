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
      name: 'The Legend of Zelda: Tears of the Kingdom',
      price: 59.99,
      image: 'https://picsum.photos/seed/zelda/300/200',
      description: 'Aventure épique dans le royaume d\'Hyrule'
    },
    {
      id: 2,
      name: 'Elden Ring',
      price: 49.99,
      image: 'https://picsum.photos/seed/eldenring/300/200',
      description: 'RPG action dans un monde ouvert'
    },
    {
      id: 3,
      name: 'God of War Ragnarök',
      price: 69.99,
      image: 'https://picsum.photos/seed/godofwar/300/200',
      description: 'Aventure mythologique nordique'
    },
    {
      id: 4,
      name: 'Hogwarts Legacy',
      price: 54.99,
      image: 'https://picsum.photos/seed/hogwarts/300/200',
      description: 'Magie et aventures à Poudlard'
    },
    {
      id: 5,
      name: 'Spider-Man 2',
      price: 64.99,
      image: 'https://picsum.photos/seed/spiderman/300/200',
      description: 'Aventure super-héroïque à New York'
    },
    {
      id: 6,
      name: 'Starfield',
      price: 59.99,
      image: 'https://picsum.photos/seed/starfield/300/200',
      description: 'Exploration spatiale et aventure'
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
