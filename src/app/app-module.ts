import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule, provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';
import { Header } from './components/header/header';
import { GameCard } from './components/game-card/game-card';
import { ShoppingCart } from './components/shopping-cart/shopping-cart';
import { CartService } from './services/cart';
import { Auth } from './components/auth/auth';
import { AuthService } from './services/auth.service';

@NgModule({
  declarations: [
    App,
    Header,
    GameCard,
    ShoppingCart,
    Auth
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    CommonModule,
    FormsModule
  ],
  providers: [
    CartService,
    AuthService,
    provideBrowserGlobalErrorListeners(),
    provideClientHydration(withEventReplay()),
  ],
  bootstrap: [App]
})
export class AppModule { }
