# Pipenvs-and-Pythons-BE

## **API Documentation**
**BACKEND URL** https://pipenvs-n-pythons.herokuapp.com/graphql/
- Direct all queries and mutations to this GraphQL endpoint
### **Table of Contents**

#### MODELS

| Model Name |
|------------|
| Player     |
| Room       |
| Map        |

#### NON-PROTECTED REQUESTS

| Request Type    | Request Name |
|-----------------|--------------|
| POST (Mutation) | createUser   |
| POST (Mutation) | tokenAuth    |

#### PROTECTED REQUESTS

| Request Type    | Request Name   |
|-----------------|----------------|
| GET (Query)     | allPlayers     |
| GET (Query)     | allRooms       |
| GET (Query)     | allMaps        |
| GET (Query)     | player         |
| GET (Query)     | room           |
| GET (Query)     | map            |
| GET (Query)     | adjacentRooms  |
| POST (Mutation) | playerMutation |

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
id = integery primary key
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

#### player

```graphql
query {
    player(id:"id") {
        player
    }
}
```

#### room

```graphql
query {
    room(id:"id") {
        room
    }
}
```

#### map

```graphql
query {
    map(id:"id") {
        map
    }
}
```

#### adjacentRoom

```graphql
query {
    adjacentRoom(id:"id") {
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
