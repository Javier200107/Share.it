import { Injectable } from '@angular/core'
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http'
import { environment } from 'src/environments/environment'
import { Observable } from 'rxjs'

import { User } from '../models/User'
import { UserLogin } from '../models/UserLogin'

@Injectable({
  providedIn: 'root'
})

export class SessionService{

  sessionToken!: string
  error!: string

  constructor (private http:HttpClient) {
  }

  setToken(token:string){
    this.sessionToken = token
  }

  register(user:User): Observable<User> {
    return this.http.post<User>(`${environment.baseApiUrl}/account`, user);
  }

  login (user:UserLogin): Observable<UserLogin> {
    console.log('Post User', user)
    return this.http.post<UserLogin>(`${environment.baseApiUrl}/login`, user)
    /* .pipe(
        catchError(err => {throw 'Error en realitzar el post '; })) */
  }
}
