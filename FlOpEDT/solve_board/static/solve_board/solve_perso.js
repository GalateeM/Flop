// This file is part of the FlOpEDT/FlOpScheduler project.
// Copyright (c) 2017
// Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// Affero General Public License for more details.
// 
// You should have received a copy of the GNU Affero General Public
// License along with this program. If not, see
// <http://www.gnu.org/licenses/>.
// 
// You can be released from the requirements of the license by purchasing
// a commercial license. Buying such a license is mandatory as soon as
// you develop activities involving the FlOpEDT/FlOpScheduler software
// without disclosing the source code of your own applications.

var lignes = [{
    id: 8, // id de la TTC
    name: "string", // nom du type de TTC
    weight: 1, // poids de la TTC
    is_active: true, // contrainte active ?
    comment: "", // commentaire sur la TTC
    last_modification:  // date de création
    weeks : [{nb: int , year: int},{nb: int , year: int}] // week a la forme : {nb: int , year: int}
    parameters : [{
        name: string, // nom du paramètre dans la TTC
        type: string, // nom du type des objets dans ce paramètre
        required: boolean, // paramètre obligatoire ?
        all_except: boolean // tous sauf ?
        id_list: list of int, // ids des objets pour le paramètre dans la TTC
        acceptable: list of int, // ids des objets acceptables comme valeur du paramètre
        }]
    },
    {
    id: 8, // id de la TTC
    name: "string", // nom du type de TTC
    weight: 1, // poids de la TTC
    is_active: true, // contrainte active ?
    comment: "", // commentaire sur la TTC
    last_modification:  // date de création
    weeks : [{nb: int , year: int},{nb: int , year: int}] // week a la forme : {nb: int , year: int}
    parameters : [{
        name: string, // nom du paramètre dans la TTC
        type: string, // nom du type des objets dans ce paramètre
        required: boolean, // paramètre obligatoire ?
        all_except: boolean // tous sauf ?
        id_list: list of int, // ids des objets pour le paramètre dans la TTC
        acceptable: list of int, // ids des objets acceptables comme valeur du paramètre
        }]
    }];

