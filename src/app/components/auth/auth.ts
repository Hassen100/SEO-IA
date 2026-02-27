import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-auth',
  standalone: false,
  templateUrl: './auth.html',
  styleUrl: './auth.css',
})
export class Auth implements OnInit {
  username = '';
  password = '';
  errorMessage = '';
  isLoading = false;
  isAuthenticated = false;
  currentUser: string | null = null;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.checkAuthStatus();
  }

  onSubmit(): void {
    if (!this.username || !this.password) {
      this.errorMessage = 'Veuillez remplir tous les champs';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    setTimeout(() => {
      if (this.authService.login(this.username, this.password)) {
        this.isAuthenticated = true;
        this.currentUser = this.authService.getCurrentUser();
        this.errorMessage = '';
      } else {
        this.errorMessage = 'Nom d\'utilisateur ou mot de passe incorrect';
      }
      this.isLoading = false;
    }, 1000);
  }

  logout(): void {
    this.authService.logout();
    this.isAuthenticated = false;
    this.currentUser = null;
    this.username = '';
    this.password = '';
  }

  private checkAuthStatus(): void {
    this.isAuthenticated = this.authService.isAuthenticated();
    if (this.isAuthenticated) {
      this.currentUser = this.authService.getCurrentUser();
    }
  }
}
