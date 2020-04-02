# Pipenvs-and-Pythons-BE

## **API Documentation**
**BACKEND URL** https://pipenvs-n-pythons.herokuapp.com/graphql/
- Direct all queries and mutations to this GraphQL endpoint
### **Table of Contents**

#### MODELS

| Model Name |
|------------|
| [Player](#Player)     |
| [Room](#Room)       |
| [Map](#Map)        |

#### NON-PROTECTED REQUESTS

| Request Type    | Request Name |
|-----------------|--------------|
| POST (Mutation) | [createUser](#createUser)   |
| POST (Mutation) | [tokenAuth](#tokenAuth)    |

#### PROTECTED REQUESTS

| Request Type    | Request Name   |
|-----------------|----------------|
| GET (Query)     | [allPlayers](#allPlayers)     |
| GET (Query)     | [allRooms](#allRooms)       |
| GET (Query)     | [allMaps](#allMaps)        |
| GET (Query)     | [player](#get-player)         |
| GET (Query)     | [room](#get-room)           |
| GET (Query)     | [map](#get-map)            |
| GET (Query)     | [adjacentRooms](#adjacentRooms)  |
| POST (Mutation) | [playerMutation](#playerMutation) |

---

### Models

#### Player

```
id = integer primary key
user_id = integer foreign key (User)
position = integer foreign key (Room)
health = integer
mana = integer
stamina = integer
```

#### Room

```
id = integer primary key
map_id = integer foreign key (Map)
name = string [max length 200]
description = string
north = integer domestic key (Room)
south = integer domestic key (Room)
east = integer domestic key (Room)
west = integer domestic key (Room)
```

#### Map

```
id = integer primary key
player_id = integer foreign key (Player)
```

---

### NON-PROTECTED REQUESTS

#### createUser

```graphql
mutation {
    createUser(username:"username", password:"password", email:"address@mail.com") {
        user
    }
}
```

#### tokenAuth

```graphql
mutation {
    tokenAuth(username:"username", password:"password") {
        token
    }
}
```

---

### PROTECTED REQUESTS

#### allPlayers

```graphql
query {
    allPlayers {
        player
    }
}
```

#### allRooms

```graphql
query {
    allRooms {
        room
    }
}
```

#### allMaps

```graphql
query {
    allMaps {
        map
    }
}
```

#### get player

```graphql
query {
    player(id:"id") {
        player
    }
}
```

#### get room

```graphql
query {
    room(id:"id") {
        room
    }
}
```

#### get map

```graphql
query {
    map(id:"id") {
        map
    }
}
```

#### adjacentRooms

```graphql
query {
    adjacentRooms(id:"id") {
        room
    }
}
```

#### playerMutation

```graphql
mutation {
    playerMutation(id:"id", [optional player fields]) {
        player
    }
}
```
