import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private isLoggedIn = false;
  private currentUser: string | null = null;

  login(username: string, password: string): boolean {
    // Simulation d'authentification simple
    if (username === 'admin' && password === 'password') {
      this.isLoggedIn = true;
      this.currentUser = username;
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('currentUser', username);
      return true;
    }
    return false;
  }

  logout(): void {
    this.isLoggedIn = false;
    this.currentUser = null;
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('currentUser');
  }

  isAuthenticated(): boolean {
    if (localStorage.getItem('isLoggedIn') === 'true') {
      this.isLoggedIn = true;
      this.currentUser = localStorage.getItem('currentUser');
    }
    return this.isLoggedIn;
  }

  getCurrentUser(): string | null {
    return this.currentUser;
  }
}
